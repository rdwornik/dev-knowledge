"""Tests for scripts/export_backlog_view.py ([#563] the one-way `Backlog.md` view layer).

Two tiers, deliberately:

  * TMP-TREE UNIT TESTS — clause splitting, frontmatter reads, filename shape, config flags,
    the wipe-and-re-render contract and its refusal guards. These build their own `tasks/`
    fixture, so they pin BEHAVIOUR and cannot be silenced by the live corpus changing.
  * `live_repo` FIDELITY TESTS — the view rendered from THIS repo's real `tasks/` tree, row
    for row. These are what the row means by "generated-view fidelity to tasks/ source":
    every task file becomes exactly one row, `## Description` carries the authoritative body
    line BYTE-FOR-BYTE, and every clause with no typed destination survives verbatim.

The three standing assertions of `[#563]`'s binding conditions live here too:
`test_nothing_under_the_export_path_is_tracked` (condition 2),
`test_no_gate_hook_or_script_reads_the_export` (condition 3), and
`test_export_writes_nothing_outside_the_export_dir` (condition 1 / Critical Rule #4).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

import export_backlog_view as ebv
from gen_task_tree import _ORPHAN_RE

REPO_ROOT = Path(__file__).resolve().parent.parent
LIVE_TASKS = REPO_ROOT / "tasks"


# --- fixtures ----------------------------------------------------------------

def _task_file_text(
    task_id: int,
    body: str,
    *,
    title: str = "A task",
    status: str = "open",
    priority: str | None = "P2",
    size: str | None = "M",
    theme: str | None = "[E2] Enforced governance",
    story: str | None = "[S4] Extend structural validation",
    serialize_group: str | None = None,
    depends_on: str | None = None,
) -> str:
    """A `tasks/<id>-<slug>.md` file in exactly the shape gen_task_tree.emit_task_file_text writes."""
    lines = ["---", f'id: "[#{task_id}]"', f"title: {json.dumps(title, ensure_ascii=False)}", f"status: {status}"]
    if priority:
        lines.append(f"priority: {priority}")
    if size:
        lines.append(f"size: {size}")
    if theme:
        lines.append(f"theme: {json.dumps(theme, ensure_ascii=False)}")
    if story:
        lines.append(f"story: {json.dumps(story, ensure_ascii=False)}")
    if serialize_group:
        lines.append(f"serialize-group: {serialize_group}")
    if depends_on:
        lines.append(f"depends-on: {json.dumps(depends_on, ensure_ascii=False)}")
    lines += ["generates: BACKLOG.md", "---", "", body]
    return "\n".join(lines) + "\n"


@pytest.fixture
def tasks_dir(tmp_path: Path) -> Path:
    d = tmp_path / "tasks"
    d.mkdir()
    (d / "1-first.md").write_text(
        _task_file_text(
            1,
            "- [#1] [P2][M] **First** — prose · Done when: it works · refs ADR-1, ADR-2 · kill-candidates: none",
            title="First",
        ),
        encoding="utf-8",
    )
    (d / "2-second.md").write_text(
        _task_file_text(
            2,
            "- [#2] [P1][S] **Second** — more prose · depends-on: #1 · serialize-group: audit-py",
            title="Second",
            status="closed",
            priority="P1",
            size="S",
            serialize_group="audit-py",
            depends_on="#1",
        ),
        encoding="utf-8",
    )
    # Not task files: the tree's own README, and the residue carrier.
    (d / "README.md").write_text("# tasks\n", encoding="utf-8")
    (d / "manifest.json").write_text("{}\n", encoding="utf-8")
    return d


def _export(tasks_dir: Path, tmp_path: Path) -> ebv.ExportResult:
    return ebv.export(tasks_dir, tmp_path / "view")


def _project(tmp_path: Path) -> Path:
    return tmp_path / "view" / ebv.PROJECT_SUBDIR


def _rendered(tmp_path: Path, task_id: int) -> str:
    return next((_project(tmp_path) / "tasks").glob(f"task-{task_id} *")).read_text(encoding="utf-8")


def _frontmatter_of(text: str) -> dict:
    assert text.startswith("---\n")
    return yaml.safe_load(text.split("\n---\n", 1)[0][4:])


def _section(text: str, heading: str) -> str | None:
    """The body of one `## <heading>` section, or None when the section is absent."""
    marker = f"\n## {heading}\n"
    if marker not in text:
        return None
    after = text.split(marker, 1)[1]
    return after.split("\n## ", 1)[0].strip("\n")


# --- clause splitting --------------------------------------------------------

def test_head_segment_is_never_a_note():
    acceptance, references, notes = ebv.split_clauses("- [#1] [P2][M] **T** — head prose only")
    assert (acceptance, references, notes) == ((), (), ())


def test_done_when_and_refs_are_typed_everything_else_is_a_note():
    acceptance, references, notes = ebv.split_clauses(
        "- [#1] head · Done when: X happens · refs ADR-1, docs/audits/a.md · kill-candidates: none · DEFER — peg"
    )
    assert acceptance == ("X happens",)
    assert references == ("ADR-1", "docs/audits/a.md")
    assert notes == ("kill-candidates: none", "DEFER — peg")


def test_multiple_done_when_clauses_each_get_their_own_box():
    acceptance, _, _ = ebv.split_clauses("- [#1] head · Done when: A · Done when: B")
    assert acceptance == ("A", "B")


# --- multi-line clauses (4 live rows carry them) -----------------------------

def test_a_multi_line_clause_stays_inside_its_list_item():
    """A bare newline would end the item: the continuation escapes the section, and one opening
    `## ` would inject a heading that truncates `## Description` for every reader downstream."""
    clause = "kill-candidates: none\n\n## NOT A HEADING\n\n**RETIRED** — prose"
    view = ebv.TaskView(id=1, title="T", status="open", body="- [#1] head", notes=(clause,))
    rendered = ebv.render_task_file(view)
    assert "\n## NOT A HEADING" not in rendered
    assert _section(rendered, "Implementation Notes") is not None
    assert ebv.dedent_item(_section(rendered, "Implementation Notes")) == clause


def test_render_item_and_dedent_item_round_trip():
    for text in ("plain", "two\nlines", "blank\n\nseparated", "trailing\n"):
        assert ebv.dedent_item(ebv.render_item(text)) == text


# --- frontmatter reads -------------------------------------------------------

def test_parse_frontmatter_recovers_json_encoded_strings():
    fm = ebv.parse_frontmatter(_task_file_text(9, "- [#9] body", title='He said "hi" — ok'))
    assert fm["id"] == 9
    assert fm["title"] == 'He said "hi" — ok'
    assert fm["theme"] == "[E2] Enforced governance"


def test_a_status_outside_the_ruled_enum_is_refused(tmp_path: Path):
    p = tmp_path / "3-x.md"
    p.write_text(_task_file_text(3, "- [#3] body", status="in-progress"), encoding="utf-8")
    with pytest.raises(ValueError, match="outside the ruled enum"):
        ebv.load_task(p)


def test_terminal_statuses_reach_the_view_and_are_not_flattened_to_open(tasks_dir: Path, tmp_path: Path):
    # The whole reason the read surface is the frontmatter: `derive_status` yields only
    # open/deferred, so reading the body would render every closed row as open.
    _export(tasks_dir, tmp_path)
    assert _frontmatter_of(_rendered(tmp_path, 2))["status"] == "closed"


# --- projection --------------------------------------------------------------

def test_ids_map_as_a_lossless_bijection(tasks_dir: Path, tmp_path: Path):
    _export(tasks_dir, tmp_path)
    ids = {_frontmatter_of(p.read_text(encoding="utf-8"))["id"] for p in (_project(tmp_path) / "tasks").iterdir()}
    assert ids == {"TASK-1", "TASK-2"}


def test_labels_and_dependencies_are_derived_from_frontmatter(tasks_dir: Path, tmp_path: Path):
    _export(tasks_dir, tmp_path)
    fm = _frontmatter_of(_rendered(tmp_path, 2))
    assert fm["labels"] == ["size:S", "theme:E2", "story:S4", "serialize-group:audit-py"]
    assert fm["dependencies"] == ["TASK-1"]


def test_references_become_a_clean_array(tasks_dir: Path, tmp_path: Path):
    _export(tasks_dir, tmp_path)
    fm = _frontmatter_of(_rendered(tmp_path, 1))
    assert fm["references"] == ["ADR-1", "ADR-2"]


def test_acceptance_boxes_are_never_pre_ticked_even_for_a_closed_row():
    view = ebv.TaskView(id=1, title="T", status="closed", body="- [#1] head · Done when: done", acceptance=("done",))
    assert "- [ ] #1 done" in ebv.render_task_file(view)
    assert "- [x]" not in ebv.render_task_file(view)


def test_empty_sections_are_omitted_rather_than_rendered_blank():
    text = ebv.render_task_file(ebv.TaskView(id=1, title="T", status="open", body="- [#1] head"))
    assert "## Description" in text
    assert "## Acceptance Criteria" not in text
    assert "## Implementation Notes" not in text


def test_a_title_with_a_quote_stays_valid_yaml():
    view = ebv.TaskView(id=1, title="it's a 'quoted' title", status="open", body="- [#1] head")
    assert _frontmatter_of(ebv.render_task_file(view))["title"] == "it's a 'quoted' title"


def test_filename_is_the_backlogmd_shape_and_is_slug_truncated():
    view = ebv.TaskView(id=7, title="A very long title " + "x" * 200, status="open", body="- [#7] head")
    name = ebv.task_filename(view)
    assert name.startswith("task-7 - ")
    assert name.endswith(".md")
    assert len(name[len("task-7 - ") : -len(".md")]) <= ebv._SLUG_MAX


# --- config ------------------------------------------------------------------

def test_config_disables_branch_checks_and_remote_operations_in_both_spellings():
    cfg = yaml.safe_load(ebv.render_config())
    for key in ("check_active_branches", "remote_operations", "checkActiveBranches", "remoteOperations"):
        assert cfg[key] is False, key


def test_config_carries_the_five_value_status_enum_verbatim():
    cfg = yaml.safe_load(ebv.render_config())
    assert cfg["statuses"] == list(ebv.STATUSES)
    assert cfg["priorities"] == list(ebv.PRIORITIES)
    assert cfg["default_status"] == "open"


def test_no_instruction_file_is_ever_written(tasks_dir: Path, tmp_path: Path):
    """`--agent-instructions none`, honoured structurally: there is no code path that emits one."""
    result = _export(tasks_dir, tmp_path)
    written = {p.name for p in result.files}
    on_disk = {p.name for p in (tmp_path / "view").rglob("*") if p.is_file()}
    for forbidden in ("AGENTS.md", "CLAUDE.md", "instructions.md", ".cursorrules", "GEMINI.md"):
        assert forbidden not in written and forbidden not in on_disk


# --- the disposable contract -------------------------------------------------

def test_re_export_is_byte_identical(tasks_dir: Path, tmp_path: Path):
    first = {p: p.read_bytes() for p in sorted(_export(tasks_dir, tmp_path).files)}
    second = {p: p.read_bytes() for p in sorted(_export(tasks_dir, tmp_path).files)}
    assert first == second


def test_re_export_removes_a_stale_row(tasks_dir: Path, tmp_path: Path):
    _export(tasks_dir, tmp_path)
    stale = _project(tmp_path) / "tasks" / "task-999 - deleted-upstream.md"
    stale.write_text("stale\n", encoding="utf-8")
    _export(tasks_dir, tmp_path)
    assert not stale.exists()


def test_re_export_reflects_a_source_edit(tasks_dir: Path, tmp_path: Path):
    _export(tasks_dir, tmp_path)
    (tasks_dir / "1-first.md").write_text(
        _task_file_text(1, "- [#1] [P2][M] **First** — EDITED · Done when: it works", title="First"),
        encoding="utf-8",
    )
    _export(tasks_dir, tmp_path)
    assert "EDITED" in _rendered(tmp_path, 1)


def test_export_refuses_a_non_empty_directory_it_did_not_generate(tasks_dir: Path, tmp_path: Path):
    victim = tmp_path / "view"
    victim.mkdir()
    (victim / "someones-real-work.txt").write_text("do not delete me\n", encoding="utf-8")
    with pytest.raises(ValueError, match="refusing to wipe"):
        ebv.export(tasks_dir, victim)
    assert (victim / "someones-real-work.txt").exists()


def test_export_refuses_a_directory_holding_a_git(tasks_dir: Path, tmp_path: Path):
    victim = tmp_path / "view"
    (victim / ".git").mkdir(parents=True)
    (victim / ebv.MARKER_NAME).write_text(ebv.MARKER_TEXT, encoding="utf-8")
    with pytest.raises(ValueError, match="contains a .git"):
        ebv.export(tasks_dir, victim)
    assert (victim / ".git").exists()


def test_export_writes_nothing_outside_the_export_dir(tasks_dir: Path, tmp_path: Path):
    """Condition 1 / Critical Rule #4: an exporter, not an orchestrator."""
    export_dir = (tmp_path / "view").resolve()

    def snapshot() -> dict[Path, bytes]:
        return {
            p: p.read_bytes()
            for p in tmp_path.rglob("*")
            if p.is_file() and export_dir not in p.resolve().parents
        }

    before = snapshot()
    assert before, "the fixture must put files outside the export dir, or this test is vacuous"
    result = _export(tasks_dir, tmp_path)
    assert all(export_dir in p.resolve().parents for p in result.files)
    assert snapshot() == before


def test_the_export_root_is_self_ignoring(tasks_dir: Path, tmp_path: Path):
    result = _export(tasks_dir, tmp_path)
    assert (tmp_path / "view" / ".gitignore").read_text(encoding="utf-8").splitlines()[-1] == "*"
    assert (tmp_path / "view" / ebv.MARKER_NAME) in result.files


def test_the_ignore_rule_is_the_first_file_written(tasks_dir: Path, tmp_path: Path):
    """No window exists in which an interrupted export has left an unignored file behind."""
    assert _export(tasks_dir, tmp_path).files[0].name == ".gitignore"


def test_the_project_level_is_where_backlogmd_looks_for_it(tasks_dir: Path, tmp_path: Path):
    """`--export-dir` is the PROJECT ROOT; config.yml and tasks/ live under `backlog/` inside it.
    Emitting them at the export root produces a view `backlog browser` cannot open at all."""
    _export(tasks_dir, tmp_path)
    assert (_project(tmp_path) / "config.yml").is_file()
    assert (_project(tmp_path) / "tasks").is_dir()
    assert not (tmp_path / "view" / "config.yml").exists()


def test_an_empty_or_mistyped_source_is_refused_before_the_wipe(tasks_dir: Path, tmp_path: Path):
    """A typo in --tasks-dir must not silently replace a live view with nothing."""
    result = _export(tasks_dir, tmp_path)
    with pytest.raises(ValueError, match="is not a directory"):
        ebv.export(tmp_path / "tsaks", tmp_path / "view")  # mistyped
    (tmp_path / "empty").mkdir()
    with pytest.raises(ValueError, match="no task files"):
        ebv.export(tmp_path / "empty", tmp_path / "view")  # right shape, wrong tree
    assert all(p.exists() for p in result.files), "the wipe ran before the source was validated"


def test_every_write_pins_the_newline(tasks_dir: Path, tmp_path: Path):
    """LF on every platform: Windows text mode would otherwise emit CRLF and break byte-comparison
    with the LF source. Swept across all of scripts/ by tests/test_generator_newlines.py."""
    for path in _export(tasks_dir, tmp_path).files:
        assert b"\r\n" not in path.read_bytes(), path


# --- live-repo fidelity ------------------------------------------------------

@pytest.fixture(scope="module")
def live_export(tmp_path_factory) -> ebv.ExportResult:
    return ebv.export(LIVE_TASKS, tmp_path_factory.mktemp("live-view") / "view")


def _live_tasks_dir(live_export: ebv.ExportResult) -> Path:
    return live_export.export_dir / ebv.PROJECT_SUBDIR / "tasks"


def _items(section: str) -> list[str]:
    """A `- ` list section split back into its clause texts (continuations de-indented)."""
    return [ebv.dedent_item("- " + chunk) for chunk in section.removeprefix("- ").split("\n- ")]


@pytest.mark.live_repo
def test_every_live_task_file_becomes_exactly_one_row(live_export):
    sources = [p for p in LIVE_TASKS.glob("*.md") if _ORPHAN_RE.match(p.name)]
    rendered = list(_live_tasks_dir(live_export).iterdir())
    assert live_export.rows == len(sources) == len(rendered)


@pytest.mark.live_repo
def test_description_carries_the_source_body_byte_for_byte(live_export):
    """The lossless carrier. If this ever fails, the view has stopped being diffable."""
    by_id = {v.id: v for v in ebv.load_tasks(LIVE_TASKS)}
    for path in _live_tasks_dir(live_export).iterdir():
        text = path.read_text(encoding="utf-8")
        task_id = int(_frontmatter_of(text)["id"].removeprefix("TASK-"))
        assert _section(text, "Description") == by_id[task_id].body


@pytest.mark.live_repo
def test_every_untyped_clause_survives_verbatim_as_an_implementation_note(live_export):
    """Round-trip, not substring: the section is split back into items and de-indented, so a
    dropped, merged or reflowed clause fails rather than hiding inside a longer match."""
    covered = 0
    for view in ebv.load_tasks(LIVE_TASKS):
        if not view.notes:
            continue
        path = _live_tasks_dir(live_export) / ebv.task_filename(view)
        section = _section(path.read_text(encoding="utf-8"), "Implementation Notes")
        assert _items(section) == list(view.notes), f"[#{view.id}] implementation notes drifted"
        covered += 1
    assert covered > 200, f"only {covered} rows carried notes — the corpus or the splitter moved"


@pytest.mark.live_repo
def test_every_done_when_clause_becomes_an_acceptance_box(live_export):
    covered = 0
    for view in ebv.load_tasks(LIVE_TASKS):
        if not view.acceptance:
            continue
        path = _live_tasks_dir(live_export) / ebv.task_filename(view)
        boxes = _items(_section(path.read_text(encoding="utf-8"), "Acceptance Criteria"))
        assert boxes == [f"[ ] #{n} {c}" for n, c in enumerate(view.acceptance, start=1)], f"[#{view.id}]"
        covered += 1
    assert covered > 200, f"only {covered} rows carried a Done-when clause"


@pytest.mark.live_repo
def test_status_and_priority_round_trip_from_the_live_tree(live_export):
    by_id = {v.id: v for v in ebv.load_tasks(LIVE_TASKS)}
    for path in _live_tasks_dir(live_export).iterdir():
        fm = _frontmatter_of(path.read_text(encoding="utf-8"))
        source = by_id[int(fm["id"].removeprefix("TASK-"))]
        assert fm["status"] == source.status
        assert fm.get("priority") == source.priority


@pytest.mark.live_repo
def test_every_exported_file_parses_as_yaml(live_export):
    for path in _live_tasks_dir(live_export).iterdir():
        _frontmatter_of(path.read_text(encoding="utf-8"))  # raises on malformed YAML
    yaml.safe_load((live_export.export_dir / ebv.PROJECT_SUBDIR / "config.yml").read_text(encoding="utf-8"))


# --- the two standing governance assertions ----------------------------------

@pytest.mark.live_repo
def test_nothing_under_the_export_path_is_tracked():
    """Condition 2. The export root is self-ignoring, so this holds with no root-.gitignore edit.

    It performs a REAL export at the shipped default path rather than probing whatever an
    earlier manual run happened to leave behind — on a clean checkout `.backlog-view/` does
    not exist, and a probe written into a bare directory is NOT ignored, so the leftover-
    dependent version of this test passed only on a machine that had already exported once.
    Critical Rule #9: a directory this test creates, this test removes.
    """
    rel = ebv.DEFAULT_EXPORT_DIR.relative_to(REPO_ROOT).as_posix()
    tracked = subprocess.run(
        ["git", "ls-files", "--", rel], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    assert tracked.stdout.strip() == "", f"{rel} has tracked files: {tracked.stdout}"

    pre_existing = ebv.DEFAULT_EXPORT_DIR.exists()
    try:
        result = ebv.export(LIVE_TASKS, ebv.DEFAULT_EXPORT_DIR)
        for path in (result.files[0], result.files[-1]):
            ignored = subprocess.run(
                ["git", "check-ignore", "-q", "--", path.relative_to(REPO_ROOT).as_posix()],
                cwd=REPO_ROOT,
                capture_output=True,
            )
            assert ignored.returncode == 0, f"{path} is NOT ignored by git"
        status = subprocess.run(
            ["git", "status", "--porcelain", "--", rel], cwd=REPO_ROOT, capture_output=True, text=True, check=True
        )
        assert status.stdout.strip() == "", f"the export dirties the tree: {status.stdout}"
    finally:
        if not pre_existing:
            # Critical Rule #9: a scratch-creating process removes AND VERIFIES
            # removal. ignore_errors=True let a failed cleanup pass green while
            # leaving the export behind -- the exact leftover this test rules out.
            shutil.rmtree(ebv.DEFAULT_EXPORT_DIR)
            assert not ebv.DEFAULT_EXPORT_DIR.exists(), (
                "cleanup left %s behind" % ebv.DEFAULT_EXPORT_DIR)


#: The enforcement surface: everything that could re-point governance at the view. `docs/`
#: is excluded on purpose — an audit artifact NAMES the export, which is not reading it.
_ENFORCEMENT_ROOTS = ("scripts", ".claude", "plugins", "deploy", "config", "ecosystem", "templates", "protocols")
_ENFORCEMENT_FILES = (".pre-commit-config.yaml", "pyproject.toml", "CLAUDE.md")
_EXPORT_TOKENS = (".backlog-view", "export_backlog_view", ebv.MARKER_NAME)
#: `.claude/worktrees/` holds FULL CHECKOUTS of this repo (ADR-61/[#107]) — descending into
#: one finds a second copy of the exporter and reds this test whenever a parallel lane is
#: live, which is a false positive about the lane, not a finding about governance. The
#: primary checkout's own copy is what this test is for.
_SKIPPED_DIRS = {".claude/worktrees", "node_modules", ".git"}


@pytest.mark.live_repo
def test_no_gate_hook_or_script_reads_the_export():
    """Condition 3: governance stays bespoke.

    HONEST LIMIT: this greps for the export's OWN names — the path, the module and the
    marker — which is the real re-pointing risk. It cannot see a gate that shells out to the
    `backlog` CLI with a path assembled at runtime.
    """
    allowed = {REPO_ROOT / "scripts" / "export_backlog_view.py", Path(__file__).resolve()}

    def _in_scope(path: Path) -> bool:
        rel = path.relative_to(REPO_ROOT).as_posix()
        return not any(rel == skip or rel.startswith(skip + "/") for skip in _SKIPPED_DIRS)

    candidates: list[Path] = [REPO_ROOT / name for name in _ENFORCEMENT_FILES]
    for root in _ENFORCEMENT_ROOTS:
        candidates.extend(p for p in (REPO_ROOT / root).rglob("*") if p.is_file() and _in_scope(p))
    assert len(candidates) > 100, "the enforcement sweep collected almost nothing — it is vacuous"

    offenders: list[str] = []
    for path in candidates:
        if not path.exists() or path.resolve() in allowed or path.suffix in {".pyc", ".lock"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for token in _EXPORT_TOKENS:
            if token in text:
                offenders.append(f"{path.relative_to(REPO_ROOT).as_posix()} references {token!r}")
    assert not offenders, "the export is read by governance: " + "; ".join(offenders)
