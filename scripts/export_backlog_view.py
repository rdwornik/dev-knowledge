#!/usr/bin/env python
"""export_backlog_view.py — [#563] the one-way `Backlog.md` view layer.

`tasks/` is the SOURCE OF TRUTH (ADR-107 §7.2, flipped by [#439]). This module renders a
DISPOSABLE `Backlog.md`-format projection of it so the Backlog.md board / web UI / search /
`overview` can be pointed at our queue unmodified. It is an EXPORTER, never an importer:
nothing here reads the view back, and no gate, hook or script is re-pointed at it.

RULED, NOT PROPOSED. `[#563]` records verdict `ADOPT-VIEW-LAYER` (2026-08-19) with three
binding conditions, all three implemented here:
  1. ONE-WAY EXPORT ONLY — `tasks/` stays the single source of truth. This module writes
     nothing outside `--export-dir` (Critical Rule #4 / ADR-28/36 Layer-2 posture).
  2. DISPOSABLE, GITIGNORED EXPORT DIR, REGENERATED PER READ — every invocation wipes and
     re-renders the whole view (`export()`), so a stale write can never be mistaken for
     truth. This is §5.4 item 1 of the trial, taken in its "re-export before every read"
     form rather than the chmod form.
  3. GOVERNANCE STAYS BESPOKE — no gate, hook or script reads the export.
     `tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export`
     is the standing assertion of (3); it greps the live enforcement surface.
Do not re-run the trial and do not propose `Backlog.md` as the store. Why it is not the
store, in one measurement (trial §4.3): `backlog task archive` frees an id, the next
`create` re-issues it, two files then carry `id: TASK-16`, and `backlog doctor` — its own
duplicate-id checker — reports clean, because the archive dir sits outside its scan.

WHY DIRECT-WRITE AND NOT THE `backlog` CLI. The CLI is NOT a write path here: it cannot set
ids (so the `[#N]` ↔ `TASK-N` bijection that keeps every ADR / commit / JOURNAL citation
resolving would be lost), it costs a node process per row, and it has a measured 170-char
title cliff (plain MAX_PATH: project root 74 + 12 + len(title) ≥ 260 → ENAMETOOLONG). Our
longest live title is 160 characters — ten characters of headroom, and the cliff moves to
~139 inside a lane worktree. Writing the on-disk format directly sidesteps all three; the
exported filename is decorative because `id:` is authoritative.

WHY `backlog/` NEVER LANDS IN THE REPO. It is ~300 generated files that duplicate `tasks/`
byte-for-byte in the description field, and ADR-101 Rule C would refuse the new top-level
home anyway (correctly). The default export dir is `.backlog-view/` and it is SELF-IGNORING:
`export()` writes a `.gitignore` containing `*` at the export root, so every file under it —
including that `.gitignore` — is invisible to git without any edit to the repo's root
`.gitignore`. Nothing under the export path can become tracked, `git status` stays clean, and
session-end backpressure is never dirtied. (The root-`.gitignore` belt-and-braces entry ships
as a fenced diff in `docs/audits/2026-08-22-technical-cloud-2-563-view-layer.md`; the
self-ignoring sentinel is what the test asserts, because it holds with no shared-file edit
and also holds for a sibling export dir outside the repo.)

NO INSTRUCTION FILE, EVER (`--agent-instructions none`). `backlog init --defaults` writes an
`AGENTS.md` — the file ADR-53 retired — whose text orders an agent to run
`backlog instructions overview` before answering and forbids editing task markdown directly.
Both directives are false in this repo: `tasks/` IS edited directly and is the source of
truth. Because this is a direct-write exporter, the flag is honoured structurally: no
instruction file is emitted at all. Asserted by `test_no_instruction_file_is_ever_written`.

THE READ SURFACE IS THE FRONTMATTER, AND THAT IS DELIBERATE. `gen_task_tree.emit_task_file_text`
templates frontmatter fresh from the body on every emit and `gen_task_tree --check` refuses a
file whose frontmatter disagrees with what its own body derives — so frontmatter is a
gate-verified projection of the body for every derivable key. It is also STRICTLY MORE than
the body carries: `derive_status` yields only open/deferred, while a retired task's
`status: closed|retired|superseded` exists only in frontmatter. Reading the body instead
would silently render 85 terminal rows as `open`.

Loose top-level module BY DESIGN (mirrors gen_audit_index.py / gen_claude_rosters.py): no
codemap node, no ARCHITECTURE codemap regen on edit.

Measured on this tree (2026-08-22, 299 task files): 664 clauses with no typed field across
279 rows. The trial's prototype measured 624 across 266 of 288 rows; the corpus has grown by
11 rows since, and the ratio is unchanged.

Emitted layout — `--export-dir` is the Backlog.md PROJECT ROOT, and the tool's own
`backlog/` level sits inside it:

    .backlog-view/
      .gitignore                 `*` — written first, so no window exists in which an
      .backlog-view-generated    interrupted run leaves an unignored file behind
      backlog/
        config.yml
        tasks/task-<N> - <slug>.md

  $ python scripts/export_backlog_view.py && backlog browser
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import yaml

# Dual import (the sibling-module shape used across scripts/): dotted for
# `python -m scripts.export_backlog_view`, bare for `python scripts/export_backlog_view.py`
# and the test path (pyproject `pythonpath` puts scripts/ on sys.path). Reuse
# gen_task_tree's body extractor and task-file predicate — never reimplement them.
try:
    from scripts.gen_task_tree import _ORPHAN_RE, extract_body
except ImportError:  # pragma: no cover - exercised by the alternate launch path
    from gen_task_tree import _ORPHAN_RE, extract_body

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
DEFAULT_TASKS_DIR = _REPO_ROOT / "tasks"
DEFAULT_EXPORT_DIR = _REPO_ROOT / ".backlog-view"

#: Backlog.md addresses a PROJECT, and a project is a directory holding a `backlog/` with
#: `config.yml` + `tasks/` inside it (trial §4.3: `backlog/tasks/*.md`, `backlog/config.yml`).
#: So `--export-dir` is the project root and the tool's own level sits one below it; writing
#: `config.yml`/`tasks/` at the export root instead produces a view the CLI cannot open.
PROJECT_SUBDIR = "backlog"

#: Marker written at the export root. `export()` refuses to wipe a directory that lacks it
#: and is non-empty — the guard that stops `--export-dir ~` from deleting someone's home.
MARKER_NAME = ".backlog-view-generated"
MARKER_TEXT = (
    "Generated by scripts/export_backlog_view.py ([#563] one-way view layer).\n"
    "Disposable: this whole directory is wiped and re-rendered on every export.\n"
    "The source of truth is tasks/. Never edit anything here; never commit it.\n"
)

#: `*` ignores every file in this directory INCLUDING this .gitignore itself, so git
#: reports no untracked path here and nothing under the export can ever become tracked.
GITIGNORE_TEXT = "# Generated view layer ([#563]) — disposable, never committed.\n*\n"

#: The five-value status enum, verbatim from `tasks/`. Backlog.md has no CLI setter for the
#: enum (`config set` refuses the key), so it is written into config.yml directly. Its own
#: terminal-status semantics do not apply to a renamed enum — `Completion: 0%` in the trial's
#: `overview` is that, not a defect, which is also why an acceptance box is never pre-ticked.
STATUSES = ("open", "deferred", "closed", "retired", "superseded")
PRIORITIES = ("P0", "P1", "P2", "P3")

_CLAUSE_SEP = " · "
_DONE_WHEN_PREFIX = "Done when:"
_REFS_PREFIX = "refs "
_REF_SPLIT_RE = re.compile(r",\s+")
_SLUG_RE = re.compile(r"[^A-Za-z0-9]+")
_SLUG_MAX = 80

#: A note or acceptance clause may span physical lines (4 live rows do). A bare newline inside
#: a `- ` item ends the list item, so continuations are indented into it — the content is
#: unchanged and `dedent_item()` recovers the clause exactly.
_ITEM_INDENT = "  "

#: `id: "[#132]"` — the one frontmatter value that is not already the scalar we want.
_ID_FM_RE = re.compile(r"^\[#(\d+)\]$")
#: `[E2] Enforced governance` -> `E2`; `[S4] …` -> `S4`. Label values are the CODE only —
#: the full theme/story text stays reachable through the verbatim Description.
_BRACKET_CODE_RE = re.compile(r"^\[([A-Z]\d+)\]")
_ID_TOKEN_RE = re.compile(r"#(\d+)")


@dataclass(frozen=True)
class TaskView:
    """One task, projected into the fields the Backlog.md on-disk format carries.

    `body` is the authoritative BACKLOG line, verbatim — the lossless carrier. Everything
    else on this dataclass is derived from it or from the gate-verified frontmatter, so the
    view is reconstructible and diffable against its source.
    """

    id: int
    title: str
    status: str
    body: str
    priority: str | None = None
    size: str | None = None
    theme: str | None = None
    story: str | None = None
    serialize_group: str | None = None
    depends_on: str | None = None
    acceptance: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def task_id(self) -> str:
        """`[#563]` -> `TASK-563`. A lossless bijection: every citation still resolves."""
        return f"TASK-{self.id}"

    @property
    def labels(self) -> tuple[str, ...]:
        out = []
        if self.size:
            out.append(f"size:{self.size}")
        for key, value in (("theme", self.theme), ("story", self.story)):
            code = _bracket_code(value)
            if code:
                out.append(f"{key}:{code}")
        if self.serialize_group:
            out.append(f"serialize-group:{self.serialize_group}")
        return tuple(out)

    @property
    def dependencies(self) -> tuple[str, ...]:
        if not self.depends_on:
            return ()
        return tuple(f"TASK-{n}" for n in _ID_TOKEN_RE.findall(self.depends_on))


def _bracket_code(value: str | None) -> str | None:
    if not value:
        return None
    m = _BRACKET_CODE_RE.match(value)
    return m.group(1) if m else None


def _frontmatter_block(file_text: str) -> str:
    """The text BETWEEN the opening `---` and its closing fence.

    Bounding the block is what makes the read safe: a task's BODY is free prose that may
    legitimately open a line with `depends-on:` or `serialize-group:`, and handing the whole
    file to a parser would let such a line be read as metadata whenever the real key is
    absent — silently fabricating a `dependencies:` id that Backlog.md's own referential
    check would then reject. No live row does this today; the bound is what keeps it that way.
    """
    if not file_text.startswith("---\n"):
        return ""
    end = file_text.find("\n---\n", 1)
    return file_text[4:end] if end != -1 else ""


def parse_frontmatter(file_text: str) -> dict[str, object]:
    """The task file's frontmatter, read with `yaml.safe_load`.

    STANDING RULING N-2 (`protocols/STANDING_RULINGS.md`, 2026-08-03): frontmatter parsing is
    `yaml.safe_load`, not a hand-rolled regex/prefix reader. The originating defect is exactly
    the class this module would have inherited — a key-class regex with no underscore silently
    dropped `reconciled_with` from a dict its own docstring called YAML frontmatter. Adopted
    here rather than diverged from; `pyyaml` is already a declared dev dependency.

    `gen_task_tree.emit_task_file_text` `json.dumps`-encodes its string values, and JSON string
    escapes are a subset of YAML's double-quoted style, so the emitted values round-trip
    unchanged. `id` is the one value that is not already the scalar we want (`"[#132]"`), so it
    is unwrapped to an int here; everything else is returned as YAML read it.
    """
    block = _frontmatter_block(file_text)
    if not block:
        return {}
    loaded = yaml.safe_load(block)
    if not isinstance(loaded, dict):
        return {}
    fields: dict[str, object] = dict(loaded)
    raw_id = fields.get("id")
    m = _ID_FM_RE.match(raw_id) if isinstance(raw_id, str) else None
    fields["id"] = int(m.group(1)) if m else None
    return fields


def split_clauses(body: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Split a BACKLOG line's `·`-delimited clauses into (acceptance, references, notes).

    The HEAD segment (id + tags + title + opening prose) is skipped: it is already carried
    verbatim by `## Description`, and counting it would make every row carry a note. Only
    `Done when:` and `refs ` have a typed destination; EVERY other clause is preserved
    verbatim as an Implementation Note, which is what keeps the projection lossless for the
    untyped vocabulary this queue actually uses (kill-candidates, DEFER, verify-first,
    amendment prose, RELOCATED markers, …).
    """
    acceptance: list[str] = []
    references: list[str] = []
    notes: list[str] = []
    for clause in body.split(_CLAUSE_SEP)[1:]:
        stripped = clause.strip()
        if stripped.startswith(_DONE_WHEN_PREFIX):
            acceptance.append(stripped[len(_DONE_WHEN_PREFIX) :].strip())
        elif stripped.startswith(_REFS_PREFIX):
            references.extend(
                ref.strip() for ref in _REF_SPLIT_RE.split(stripped[len(_REFS_PREFIX) :].strip()) if ref.strip()
            )
        else:
            notes.append(clause)
    return tuple(acceptance), tuple(references), tuple(notes)


def load_task(path: Path) -> TaskView:
    """Project one `tasks/<id>-<slug>.md` file into a TaskView. Raises on a malformed file."""
    text = path.read_text(encoding="utf-8")
    body = extract_body(text)
    fm = parse_frontmatter(text)
    task_id = fm.get("id")
    if not isinstance(task_id, int):
        raise ValueError(f"{path.name}: no parsable `id: \"[#N]\"` frontmatter key")
    status = fm.get("status")
    if status not in STATUSES:
        raise ValueError(f"{path.name}: status {status!r} is outside the ruled enum {STATUSES}")
    acceptance, references, notes = split_clauses(body)
    return TaskView(
        id=task_id,
        title=str(fm.get("title") or f"task {task_id}"),
        status=str(status),
        body=body,
        priority=fm.get("priority"),  # type: ignore[arg-type]
        size=fm.get("size"),  # type: ignore[arg-type]
        theme=fm.get("theme"),  # type: ignore[arg-type]
        story=fm.get("story"),  # type: ignore[arg-type]
        serialize_group=fm.get("serialize-group"),  # type: ignore[arg-type]
        depends_on=fm.get("depends-on"),  # type: ignore[arg-type]
        acceptance=acceptance,
        references=references,
        notes=notes,
    )


def load_tasks(tasks_dir: Path) -> list[TaskView]:
    """Every task file in `tasks/`, id-ordered. `tasks/README.md` and `manifest.json` are not
    task files and are excluded by `gen_task_tree._ORPHAN_RE`, the same predicate the tree
    gate uses — so this enumeration cannot drift from the source-of-truth's own."""
    if not tasks_dir.is_dir():
        raise ValueError(f"--tasks-dir {tasks_dir} is not a directory")
    paths = sorted(p for p in tasks_dir.glob("*.md") if _ORPHAN_RE.match(p.name))
    if not paths:
        # An empty result is never a legitimate export: it means the source was mistyped or
        # moved. Refusing here is what stops `--tasks-dir tsaks` from wiping a live view and
        # reporting "exported 0 rows" with exit 0 — a silent replacement of the view by nothing.
        raise ValueError(f"{tasks_dir} contains no task files — refusing to export an empty view")
    views = [load_task(p) for p in paths]
    seen: set[int] = set()
    for view in views:
        if view.id in seen:
            raise ValueError(f"duplicate task id [#{view.id}] in {tasks_dir}")
        seen.add(view.id)
    return sorted(views, key=lambda v: v.id)


def render_item(text: str) -> str:
    """One markdown list item carrying `text`, continuations folded into the item.

    A clause that spans physical lines would otherwise terminate the list at its first
    newline — the paragraph after it escapes the section, and a continuation that happened to
    open with `## ` would inject a heading and truncate `## Description` for every reader
    downstream. Indenting is the only transformation applied; `dedent_item` is its inverse.
    """
    return "- " + text.replace("\n", "\n" + _ITEM_INDENT)


def dedent_item(item: str) -> str:
    """Inverse of `render_item`: recover the clause text from a rendered list item."""
    return item.removeprefix("- ").replace("\n" + _ITEM_INDENT, "\n")


def _yaml_quote(value: str) -> str:
    """YAML single-quoted scalar: the one style that needs no escape table (only `'` doubles)."""
    return "'" + value.replace("'", "''") + "'"


def _flow_seq(values) -> str:
    return "[" + ", ".join(_yaml_quote(v) for v in values) + "]"


def task_filename(view: TaskView) -> str:
    """`task-<N> - <slug>.md`, the Backlog.md filename shape. Decorative: `id:` is authoritative,
    which is why truncating the slug at 80 chars is safe and keeps us far off the MAX_PATH cliff."""
    slug = _SLUG_RE.sub("-", view.title).strip("-")[:_SLUG_MAX].strip("-")
    return f"task-{view.id} - {slug or 'task'}.md"


def render_task_file(view: TaskView) -> str:
    """One exported task file: Backlog.md frontmatter + the three-heading body."""
    lines = ["---", f"id: {view.task_id}", f"title: {_yaml_quote(view.title)}", f"status: {view.status}"]
    if view.priority:
        lines.append(f"priority: {view.priority}")
    if view.labels:
        lines.append(f"labels: {_flow_seq(view.labels)}")
    if view.dependencies:
        lines.append(f"dependencies: {_flow_seq(view.dependencies)}")
    if view.references:
        lines.append("references:")
        lines.extend(f"  - {_yaml_quote(ref)}" for ref in view.references)
    lines.append("---")

    # `## Description` carries the WHOLE authoritative body line, verbatim — the lossless
    # carrier that makes the view diffable against tasks/. Nothing is dropped or reflowed.
    lines += ["", "## Description", "", view.body]
    if view.acceptance:
        # Never pre-ticked: the box is not a completion signal here, `status:` is. Backlog.md
        # computes completion against a status it recognises as terminal and our renamed enum
        # contains no such status, so a tick would assert something the tool cannot mean.
        lines += ["", "## Acceptance Criteria", ""]
        lines += [render_item(f"[ ] #{n} {text}") for n, text in enumerate(view.acceptance, start=1)]
    if view.notes:
        lines += ["", "## Implementation Notes", ""]
        lines += [render_item(note) for note in view.notes]
    return "\n".join(lines) + "\n"


def render_config() -> str:
    """`backlog/config.yml` — the two hazard mitigations the row names, plus the enum.

    BOTH SPELLINGS OF THE TWO FLAGS ARE EMITTED, deliberately. `[#563]` names them
    snake_case and that is the binding wording; the trial observed the live file using
    camelCase (`checkActiveBranches: true` with `remoteOperations: true` by default, which
    costs ~2.8s of git chatter on every read and is the reason they are turned off). Unknown
    keys are inert, so writing the pair guarantees the setting binds whichever spelling the
    reader looks for — a one-line cost against a silently-ineffective mitigation.
    """
    return (
        "# GENERATED — scripts/export_backlog_view.py ([#563]). Disposable, never committed.\n"
        "# Re-rendered on every export; edits here are lost. Source of truth: tasks/.\n"
        "projectName: 'dev-knowledge (read-only view)'\n"
        f"statuses: {_flow_seq(STATUSES)}\n"
        f"priorities: {_flow_seq(PRIORITIES)}\n"
        "default_status: 'open'\n"
        "check_active_branches: false\n"
        "remote_operations: false\n"
        "checkActiveBranches: false\n"
        "remoteOperations: false\n"
    )


@dataclass(frozen=True)
class ExportResult:
    export_dir: Path
    rows: int
    files: tuple[Path, ...]
    seconds: float


def _prepare_export_dir(export_dir: Path) -> None:
    """Wipe-and-recreate, with the guard that makes a disposable dir safe to wipe.

    Refuses a non-empty directory that this exporter did not generate (no MARKER_NAME), and
    refuses outright anything holding a `.git` — the two ways `--export-dir` could otherwise
    be pointed at real work.
    """
    if export_dir.exists():
        if not export_dir.is_dir():
            raise ValueError(f"--export-dir {export_dir} exists and is not a directory")
        if (export_dir / ".git").exists():
            raise ValueError(f"refusing to wipe {export_dir}: it contains a .git")
        contents = list(export_dir.iterdir())
        if contents and not (export_dir / MARKER_NAME).is_file():
            raise ValueError(
                f"refusing to wipe {export_dir}: it is non-empty and carries no {MARKER_NAME} marker, "
                "so it was not generated by this exporter"
            )
        shutil.rmtree(export_dir)
    export_dir.mkdir(parents=True)


def export(tasks_dir: Path = DEFAULT_TASKS_DIR, export_dir: Path = DEFAULT_EXPORT_DIR) -> ExportResult:
    """Render the whole view. Wipes first, so the result is a function of `tasks/` alone.

    Layer-2 posture: the ONLY paths written are inside `export_dir`.
    """
    started = time.perf_counter()
    views = load_tasks(tasks_dir)  # refuses BEFORE the wipe, so a bad --tasks-dir costs nothing
    _prepare_export_dir(export_dir)
    written: list[Path] = []

    def _write(path: Path, text: str) -> None:
        # newline="\n" on every write: without it, Windows text mode rewrites LF to CRLF and
        # the emitted view stops being byte-comparable with its LF source. Pinned across all
        # of scripts/ by tests/test_generator_newlines.py.
        path.write_text(text, encoding="utf-8", newline="\n")
        written.append(path)

    # The ignore rule lands FIRST. Written after the marker, an interrupted run would leave an
    # unignored file behind and dirty `git status` — the one failure this design exists to rule out.
    _write(export_dir / ".gitignore", GITIGNORE_TEXT)
    _write(export_dir / MARKER_NAME, MARKER_TEXT)

    project = export_dir / PROJECT_SUBDIR
    project.mkdir()
    _write(project / "config.yml", render_config())

    task_out = project / "tasks"
    task_out.mkdir()
    for view in views:
        _write(task_out / task_filename(view), render_task_file(view))

    return ExportResult(
        export_dir=export_dir,
        rows=len(views),
        files=tuple(written),
        seconds=time.perf_counter() - started,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--tasks-dir", type=Path, default=DEFAULT_TASKS_DIR, help="source of truth (default: tasks/)")
    parser.add_argument(
        "--export-dir",
        type=Path,
        default=DEFAULT_EXPORT_DIR,
        help="disposable view root; wiped and re-rendered on every run (default: .backlog-view/)",
    )
    parser.add_argument("--quiet", action="store_true", help="suppress the summary line")
    args = parser.parse_args(argv)

    try:
        result = export(args.tasks_dir, args.export_dir)
    except (OSError, ValueError) as exc:
        print(f"export_backlog_view: {exc}", file=sys.stderr)
        return 2

    if not args.quiet:
        per_row = result.seconds / result.rows * 1000 if result.rows else 0.0
        print(
            f"exported {result.rows} rows in {result.seconds:.2f}s ({per_row:.1f} ms/row) "
            f"-> {result.export_dir}"
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
