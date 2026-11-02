from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import system_map  # noqa: E402
import system_view  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NOW = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)
READER_IDS = (
    "map-json",
    "map-record",
    "p1-mermaid",
    "launch-receipts",
    "phase-receipts",
    "merge-receipts",
    "ledger",
    "conductor-metrics",
    "quota",
    "health",
    "verdicts",
    "tasks",
)
TIMESTAMPED = {
    "launch-receipts": "launched_at",
    "phase-receipts": "finished_at",
    "merge-receipts": "closed",
    "quota": "measured",
}
SCHEDULED_READERS = {"map-record", "merge-receipts"}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_json(path: Path, data: object) -> None:
    _write(path, json.dumps(data, sort_keys=True) + "\n")


def _ledger_data() -> dict:
    return {
        "head": "head-sha",
        "main": "main-sha",
        "open_rows": [],
        "blocked": [],
        "worktrees": [],
        "open_batches": [],
        "proposal": None,
    }


def _conductor_data() -> dict:
    return {
        "n1_automated_transitions": 1,
        "n2_operator_hours": 2,
        "n3_operator_pastes": 3,
        "n4_organs_deleted": 4,
        "n5_actions_minutes": 5,
    }


def _set_seams(
    monkeypatch: pytest.MonkeyPatch,
    *,
    ledger: dict | None = None,
    conductor: dict | None = None,
) -> None:
    ledger_data = _ledger_data() if ledger is None else ledger
    conductor_data = _conductor_data() if conductor is None else conductor
    monkeypatch.setattr(system_view, "_ledger_collect", lambda root: ledger_data)
    monkeypatch.setattr(system_view, "_conductor_metrics", lambda root: conductor_data)


def _source_payload(reader_id: str, *, title: str = "T") -> object:
    launched = NOW.isoformat()
    payloads = {
        "map-json": {
            "schema": "system-map/1",
            "meta": {
                "leaf_count": 1,
                "organ_count": 2,
                "dead_count": 0,
                "unexplained_count": 0,
            },
        },
        "map-record": {
            "map_sha": "a" * 64,
            "node_count": 3,
            "previous_sha": "c" * 64,
            "diff": {"added_count": 0, "removed_count": 0},
        },
        "launch-receipts": {
            "slug": "x",
            "launched_at": launched,
            "batch": "b",
            "kind": "k",
            "attempt": 1,
            "model_requested": "model",
            "job_id": "job",
        },
        "phase-receipts": {
            "lane": "x",
            "phase": "p",
            "status": "complete",
            "finished_at": launched,
            "round": 1,
            "served_model": "model",
            "vendor": "vendor",
        },
        "merge-receipts": {
            "slug": "x",
            "merge_sha": "b" * 40,
            "closed": launched,
            "batch": "b",
            "kind": "k",
            "recorded_seconds": 1,
        },
        "quota": {
            "group": "g",
            "cycle": "2026-11-01",
            "used": 1.0,
            "quota": 10.0,
            "pct": 10.0,
            "billed": 1.0,
            "measured": launched,
        },
        "verdicts": {
            "rows": [{"provider": "p", "verdict": "parity"}],
            "row": "[#785]",
            "generated_by": "x",
        },
        "tasks": {"id": "[#1]", "title": title, "status": "open", "priority": "P2"},
    }
    return payloads.get(reader_id)


def _reader_path(root: Path, reader_id: str) -> Path | None:
    paths = {
        "map-json": root / "ecosystem" / "system-map.json",
        "map-record": root / "ecosystem" / "system-map-record.json",
        "p1-mermaid": root / "ecosystem" / "process-binding.yaml",
        "launch-receipts": root / "logs" / "receipts" / "LAUNCH-X.json",
        "phase-receipts": root / "logs" / "receipts" / "LANE-x" / "r1" / "p.json",
        "merge-receipts": root / "logs" / "MERGE-RECEIPTS.jsonl",
        "quota": Path(os.environ["DEV_KNOWLEDGE_QUOTA_READS_LEDGER"]),
        "verdicts": root / "logs" / "PROVIDER-VERDICTS.json",
        "tasks": root / "tasks" / "1-x.md",
    }
    return paths.get(reader_id)


def _write_reader(root: Path, reader_id: str, *, title: str = "T") -> None:
    if reader_id in {"ledger", "conductor-metrics", "health"}:
        return
    path = _reader_path(root, reader_id)
    assert path is not None
    payload = _source_payload(reader_id, title=title)
    if reader_id == "p1-mermaid":
        _write(
            path,
            "schema: x\ndiagram_mermaid: |\n"
            "  stateDiagram-v2\n      a --> b\n",
        )
    elif reader_id == "merge-receipts":
        _write(path, json.dumps(payload) + "\n")
    elif reader_id == "quota":
        _write(path, json.dumps(payload) + "\n")
    elif reader_id == "tasks":
        frontmatter = "\n".join(f'{key}: "{value}"' for key, value in payload.items())
        _write(path, f"---\n{frontmatter}\n---\nbody\n")
    else:
        _write_json(path, payload)


def _fixture_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    name: str = "repo",
    title: str = "T",
) -> Path:
    root = tmp_path / name
    root.mkdir()
    quota_path = root / "quota-reads.jsonl"
    monkeypatch.setenv("DEV_KNOWLEDGE_QUOTA_READS_LEDGER", str(quota_path))
    _set_seams(monkeypatch)
    for reader_id in READER_IDS:
        _write_reader(root, reader_id, title=title)
    return root


def _remove_reader_source(root: Path, reader_id: str) -> None:
    if reader_id in {"ledger", "conductor-metrics", "health"}:
        return
    path = _reader_path(root, reader_id)
    assert path is not None
    if path.exists():
        path.unlink()


def _drop_field(
    root: Path,
    reader_id: str,
    field: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if reader_id in {"ledger", "conductor-metrics"}:
        data = _ledger_data() if reader_id == "ledger" else _conductor_data()
        data.pop(field, None)
        if reader_id == "ledger":
            _set_seams(monkeypatch, ledger=data)
        else:
            _set_seams(monkeypatch, conductor=data)
        return

    path = _reader_path(root, reader_id)
    assert path is not None
    if reader_id == "p1-mermaid":
        _write(path, "schema: x\n")
        return
    if reader_id == "tasks":
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        data = yaml.safe_load(frontmatter)
    elif reader_id == "merge-receipts" or reader_id == "quota":
        data = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    parts = field.split(".")
    target = data
    for part in parts[:-1]:
        if not isinstance(target, dict) or part not in target:
            target = data
            break
        target = target[part]
    if isinstance(target, dict) and parts[-1] in target:
        target.pop(parts[-1])
    else:
        def remove_key(value: object) -> bool:
            if isinstance(value, dict):
                if field in value:
                    value.pop(field)
                    return True
                return any(remove_key(child) for child in value.values())
            if isinstance(value, list):
                return any(remove_key(child) for child in value)
            return False

        assert remove_key(data), f"could not remove {field!r} from {reader_id}"
    if reader_id == "tasks":
        frontmatter = "\n".join(f"{key}: {value!r}" for key, value in data.items())
        _write(path, f"---\n{frontmatter}\n---\nbody\n")
    elif reader_id in {"merge-receipts", "quota"}:
        _write(path, json.dumps(data) + "\n")
    else:
        _write_json(path, data)


def _read(reader_id: str, root: Path) -> list[dict]:
    return system_view.read_source(reader_id, root, now=NOW)


def _tile(reader_id: str, root: Path) -> dict:
    tiles = _read(reader_id, root)
    assert tiles
    return tiles[0]


def _all_cells(value: object) -> list[dict]:
    cells: list[dict] = []
    if isinstance(value, dict):
        if "v" in value and "r" in value:
            cells.append(value)
        for child in value.values():
            cells.extend(_all_cells(child))
    elif isinstance(value, list):
        for child in value:
            cells.extend(_all_cells(child))
    return cells


def _data_strings(value: object) -> set[str]:
    values: set[str] = set()
    if isinstance(value, dict):
        for child in value.values():
            values.update(_data_strings(child))
    elif isinstance(value, list):
        for child in value:
            values.update(_data_strings(child))
    elif value is not None and not isinstance(value, bool):
        values.add(str(value))
    return values


class _MarkupParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_script_or_style = False
        self.snapshot = False
        self.snapshot_text = ""
        self.text_nodes: list[str] = []
        self.attributes: list[tuple[str, str]] = []
        self.pre_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag in {"script", "style"}:
            self.in_script_or_style = True
            self.snapshot = (
                tag == "script"
                and attr_map.get("type") == "application/json"
            )
        if tag == "pre":
            self.pre_text = ""
        for name, value in attrs:
            if value is not None:
                self.attributes.append((name, value))
            if name == "data-p" and value is not None:
                assert re.fullmatch(r"[a-z0-9_.]+", value)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.in_script_or_style = False
            self.snapshot = False

    def handle_data(self, data: str) -> None:
        if self.snapshot:
            self.snapshot_text += data
        elif not self.in_script_or_style and data.strip():
            self.text_nodes.append(data.strip())
        if not self.in_script_or_style:
            self.pre_text += data


def _parse_html(text: str) -> _MarkupParser:
    parser = _MarkupParser()
    parser.feed(text)
    parser.close()
    return parser


def _assert_data_only_markup(view: dict, html: str) -> _MarkupParser:
    parser = _parse_html(html)
    allowed = _data_strings(view) | set(system_view.LABELS.values())
    assert parser.text_nodes
    assert all(text in allowed for text in parser.text_nodes)
    for name, value in parser.attributes:
        if name == "data-p":
            current: object = view
            for part in value.split("."):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                elif isinstance(current, list) and part.isdigit():
                    current = current[int(part)]
                else:
                    pytest.fail(f"data-p path does not resolve: {value}")
        else:
            assert value in allowed
    return parser


def test_cli_view_writes_both_outputs(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    out_dir = tmp_path / "out"
    result = CliRunner().invoke(
        system_map.cli,
        [
            "view",
            "--leg",
            "fast",
            "--repo-root",
            str(root),
            "--out-dir",
            str(out_dir),
            "--now",
            NOW.isoformat(),
        ],
    )
    assert result.exit_code == 0, result.output
    assert (out_dir / "view.json").is_file()
    assert (out_dir / "view.html").is_file()


def test_two_renders_are_byte_identical(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    first = system_view.assemble(root, now=NOW)
    second = system_view.assemble(root, now=NOW)
    assert system_view.render_json(first) == system_view.render_json(second)
    assert system_view.render_html(first) == system_view.render_html(second)
    assert system_view.render_json(first) == system_view.render_json(
        system_view.assemble(root, now=NOW)
    )


def test_every_text_node_and_attribute_is_data_or_label(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)
    parser = _assert_data_only_markup(view, system_view.render_html(view))
    assert len(parser.text_nodes) >= 30
    assert len(system_view.LABELS) <= 120
    assert all(len(value) <= 80 for value in system_view.LABELS.values())


def test_pins():
    pins = json.loads(
        (ROOT / "tests" / "fixtures" / "system_view" / "pins.json").read_text(
            encoding="utf-8"
        )
    )
    labels = json.dumps(
        system_view.LABELS,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("ascii")
    thresholds = json.dumps(
        system_view.THRESHOLDS,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("ascii")
    assert pins["labels_sha256"] == hashlib.sha256(labels).hexdigest()
    assert pins["thresholds_sha256"] == hashlib.sha256(thresholds).hexdigest()
    assert pins["script_sha256"] == hashlib.sha256(
        system_view.PAGE_SCRIPT.encode("utf-8")
    ).hexdigest()
    assert pins["css_sha256"] == hashlib.sha256(
        system_view.PAGE_CSS.encode("utf-8")
    ).hexdigest()


def test_assembly_refuses_a_value_with_no_reader_id(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    invalid_missing = {"readers": list(READER_IDS), "data": {"v": "x"}}
    invalid_unknown = {
        "readers": list(READER_IDS),
        "data": {"v": "x", "r": "not-a-reader"},
    }
    with pytest.raises(system_view.ProvenanceError):
        system_view.check_provenance(invalid_missing)
    with pytest.raises(system_view.ProvenanceError):
        system_view.check_provenance(invalid_unknown)

    def bad_reader(root, *, now, siblings=(), map_json=None):
        return [{"id": "bad", "source": {"v": "x"}, "fields": [], "rows": []}]

    monkeypatch.setitem(system_view.READERS, "map-json", bad_reader)
    with pytest.raises(system_view.ProvenanceError):
        system_view.assemble(root, now=NOW)


def test_reader_ids_are_the_frozen_set():
    assert set(system_view.READERS) == set(READER_IDS)


@pytest.mark.parametrize(
    "reader_id",
    [reader for reader in READER_IDS if reader not in {"health", "ledger", "conductor-metrics"}],
    ids=lambda reader: reader,
)
def test_source_reader_is_absent_when_its_source_is_missing(
    reader_id, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    _remove_reader_source(root, reader_id)
    assert _tile(reader_id, root)["state"]["v"] == "ABSENT"


_REQUIRED_FIELDS = [
    (reader_id, field)
    for reader_id in READER_IDS
    if reader_id != "health"
    for field in system_view.SOURCES[reader_id]["required"]
]


@pytest.mark.parametrize(
    "reader_id,field",
    _REQUIRED_FIELDS,
    ids=[f"{reader}-{field}" for reader, field in _REQUIRED_FIELDS],
)
def test_missing_required_fields_are_unreadable(
    reader_id, field, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    _drop_field(root, reader_id, field, monkeypatch)
    assert _tile(reader_id, root)["state"]["v"] == "UNREADABLE"


_OPTIONAL_FIELDS = [
    (reader_id, field)
    for reader_id in READER_IDS
    if reader_id != "health"
    for field in system_view.SOURCES[reader_id]["optional"]
]


@pytest.mark.parametrize(
    "reader_id,field",
    _OPTIONAL_FIELDS,
    ids=[f"{reader}-{field}" for reader, field in _OPTIONAL_FIELDS],
)
def test_missing_optional_fields_do_not_change_ok_state(
    reader_id, field, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    _drop_field(root, reader_id, field, monkeypatch)
    assert _tile(reader_id, root)["state"]["v"] == "OK"


@pytest.mark.parametrize("reader_id,timestamp_field", TIMESTAMPED.items())
def test_timestamped_readers_boundary(
    reader_id, timestamp_field, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    age = system_view.THRESHOLDS[reader_id]
    assert age == system_view.SOURCES[reader_id]["max_age"]

    path = _reader_path(root, reader_id)
    assert path is not None
    for offset, expected in ((age - 1, "OK"), (age + 1, "STALE")):
        _write_reader(root, reader_id)
        if reader_id in {"merge-receipts", "quota"}:
            data = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
            data[timestamp_field] = (NOW - timedelta(seconds=offset)).isoformat()
            _write(path, json.dumps(data) + "\n")
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            data[timestamp_field] = (NOW - timedelta(seconds=offset)).isoformat()
            _write_json(path, data)
        tile = _tile(reader_id, root)
        assert tile["state"]["v"] == expected
        assert tile["staleness"]["v"] == expected


@pytest.mark.parametrize(
    "reader_id",
    [reader for reader in READER_IDS if reader not in TIMESTAMPED],
    ids=lambda reader: reader,
)
def test_untimestamped_reader_is_not_computed_never_stale(
    reader_id, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    old_mtime = datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp()
    for path in root.rglob("*"):
        if path.is_file():
            os.utime(path, (old_mtime, old_mtime))
    tile = _tile(reader_id, root)
    assert tile["staleness"]["v"] == "NOT COMPUTED"
    assert tile["state"]["v"] != "STALE"
    if reader_id == "health":
        assert tile["state"]["v"] == "NOT COMPUTED"


def test_thresholds_table_is_bounded_and_pinned_in_one_place(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    assert set(system_view.THRESHOLDS) == set(TIMESTAMPED)
    assert all(
        isinstance(age, int) and 0 < age <= 31 * 86400
        for age in system_view.THRESHOLDS.values()
    )
    assert {
        key: cell["v"]
        for key, cell in system_view.assemble(root, now=NOW)["thresholds"].items()
    } == system_view.THRESHOLDS


def test_git_check_ignore_holds_for_both_outputs():
    for path in ("ecosystem/view.json", "ecosystem/view.html"):
        result = subprocess.run(
            ["git", "check-ignore", "-q", path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr


def test_live_and_frozen_modes_parse_and_compare_equal(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)
    out_dir = tmp_path / "out"
    system_view.write_outputs(view, out_dir)
    html = (out_dir / "view.html").read_text(encoding="utf-8")
    snapshot = _parse_html(html).snapshot_text
    assert json.loads(snapshot) == json.loads(
        (out_dir / "view.json").read_bytes()
    )


def test_snapshot_escapes_every_less_than(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch, title="</script><b>x")
    view = system_view.assemble(root, now=NOW)
    html = system_view.render_html(view)
    snapshot = _parse_html(html).snapshot_text
    assert "<" not in snapshot
    assert json.loads(snapshot) == view
    assert "</script><b>" not in html


def test_page_script_replaces_snapshot_only_after_a_successful_parse():
    refresh = "try{var n=JSON.parse(t);D=n;paint();}catch(e){}"
    assert system_view.PAGE_SCRIPT.count(refresh) == 1
    assert re.search(r"catch\(e\)\{\}", system_view.PAGE_SCRIPT)


def test_page_script_has_no_literal_beyond_keys_and_selectors():
    literals = re.findall(r"""(['"])(.*?)\1""", system_view.PAGE_SCRIPT)
    values = [value for _, value in literals]
    assert all(value in system_view.SCRIPT_LITERALS for value in values)
    assert len(system_view.SCRIPT_LITERALS) <= 16
    assert all(len(value) <= 24 and not re.search(r"\s", value) for value in values)
    assert all(
        len(value) <= 24 and not re.search(r"\s", value)
        for value in system_view.SCRIPT_LITERALS
    )


def test_mermaid_is_sri_pinned_and_only_in_served_mode(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)
    mermaid = system_view.MERMAID
    assert mermaid["integrity"].startswith("sha384-")
    assert mermaid["url"].startswith("https://")
    assert mermaid["version"]
    assert all(
        view["mermaid"][key]["v"] == value for key, value in mermaid.items()
    )
    html = system_view.render_html(view)
    assert "<script src=" not in html
    assert "integrity=" not in html
    assert "location.protocol" in system_view.PAGE_SCRIPT
    assert "integrity" in system_view.PAGE_SCRIPT
    parser = _parse_html(html)
    assert "stateDiagram-v2" in parser.pre_text


def _tree_listing(root: Path) -> list[tuple[str, int, int]]:
    return sorted(
        (
            str(path.relative_to(root)),
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for path in root.rglob("*")
        if path.is_file()
    )


def test_sibling_worktree_receipt_tile_names_its_checkout_and_is_read_only(
    tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch, name="current")
    sibling = _fixture_repo(tmp_path, monkeypatch, name="sibling")
    before = _tree_listing(sibling)
    view = system_view.assemble(root, now=NOW, siblings=(sibling,))
    tiles = [tile for tile in view["tiles"] if tile["reader"] == "launch-receipts"]
    assert len(tiles) == 2
    checkouts = {tile["checkout"]["v"] for tile in tiles}
    assert checkouts == {root.name, sibling.name}
    assert _tree_listing(sibling) == before


def test_task_title_pair_is_cut_and_marked_as_source_text(tmp_path, monkeypatch):
    title = "x" * 300
    root = _fixture_repo(tmp_path, monkeypatch, title=title)
    view = system_view.assemble(root, now=NOW)
    title_cells = [cell for cell in _all_cells(view) if cell.get("src")]
    assert len(title_cells) == 1
    assert title_cells[0]["v"] == title[:100]
    assert len(title_cells[0]["v"]) == 100
    assert system_view.FREE_TEXT_ALLOWLIST == (("tasks", "title"),)
    assert system_view.TITLE_MAX == 100
    html = system_view.render_html(view)
    assert title[:100] in html


def test_scheduled_leg_reads_only_the_record_and_merge_receipts(
    tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    called: set[str] = set()
    original = dict(system_view.READERS)
    for reader_id in READER_IDS:
        if reader_id not in SCHEDULED_READERS:
            monkeypatch.setitem(
                system_view.READERS,
                reader_id,
                lambda *args, _id=reader_id, **kwargs: pytest.fail(
                    f"scheduled leg called {_id}"
                ),
            )
        else:
            def tracked(*args, _id=reader_id, **kwargs):
                called.add(_id)
                return original[_id](*args, **kwargs)

            monkeypatch.setitem(system_view.READERS, reader_id, tracked)

    view = system_view.assemble(root, now=NOW, leg="scheduled")
    assert called == SCHEDULED_READERS
    not_computed = {
        tile["reader"]: tile
        for tile in view["tiles"]
        if tile["reader"] not in SCHEDULED_READERS
    }
    assert set(not_computed) == set(READER_IDS) - SCHEDULED_READERS
    assert all(tile["state"]["v"] == "NOT COMPUTED" for tile in not_computed.values())
    assert all(
        tile["reason"]["v"] == "leg-scheduled" for tile in not_computed.values()
    )


@pytest.mark.parametrize("leg", ["fast", "scheduled"])
def test_fast_leg_never_calls_build_map(tmp_path, monkeypatch, leg):
    root = _fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(
        system_map,
        "build_map",
        lambda *args, **kwargs: pytest.fail("view leg called build_map"),
    )
    monkeypatch.setattr(
        system_map,
        "write_outputs",
        lambda *args, **kwargs: pytest.fail("view leg called map write_outputs"),
    )
    result = CliRunner().invoke(
        system_map.cli,
        ["view", "--leg", leg, "--repo-root", str(root), "--now", NOW.isoformat()],
    )
    assert result.exit_code == 0, result.output


def test_full_leg_builds_the_map_once_then_the_view(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    out_dir = tmp_path / "out"
    calls: list[tuple[tuple, dict]] = []

    def write_map(*args, **kwargs):
        calls.append((args, kwargs))
        target = Path(kwargs.get("out_dir", args[1] if len(args) > 1 else out_dir))
        _write_json(
            target / "system-map.json",
            {
                "schema": "system-map/1",
                "meta": {
                    "leaf_count": 1,
                    "organ_count": 2,
                    "dead_count": 0,
                    "unexplained_count": 0,
                },
            },
        )
        return {"map_sha": "a" * 64, "node_count": 3}

    monkeypatch.setattr(system_map, "write_outputs", write_map)
    result = CliRunner().invoke(
        system_map.cli,
        [
            "view",
            "--leg",
            "full",
            "--repo-root",
            str(root),
            "--out-dir",
            str(out_dir),
            "--now",
            NOW.isoformat(),
        ],
    )
    assert result.exit_code == 0, result.output
    assert len(calls) == 1
    assert (out_dir / "view.json").is_file()


def test_system_view_imports_only_stdlib_and_the_named_first_party_modules():
    path = ROOT / "scripts" / "system_view.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    first_party = {"gen_ledger", "conductor", "quota_watch"}

    class ImportVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.function_depth = 0

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.function_depth += 1
            self.generic_visit(node)
            self.function_depth -= 1

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                root_name = alias.name.split(".", 1)[0]
                if self.function_depth:
                    assert root_name in sys.stdlib_module_names | first_party
                else:
                    assert root_name in sys.stdlib_module_names

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            if node.module is None:
                assert self.function_depth
                return
            root_name = node.module.split(".", 1)[0]
            if self.function_depth:
                assert root_name in sys.stdlib_module_names | first_party
            else:
                assert root_name in sys.stdlib_module_names

    ImportVisitor().visit(tree)


def test_write_outputs_is_atomic(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    replacements: list[tuple[str, str]] = []
    real_replace = os.replace

    def record_replace(source, destination):
        replacements.append((str(source), str(destination)))
        return real_replace(source, destination)

    monkeypatch.setattr(system_view.os, "replace", record_replace)
    system_view.write_outputs(view, out_dir)
    assert any(Path(destination) == out_dir / "view.json" for _, destination in replacements)
    assert {path.name for path in out_dir.iterdir()} == {"view.json", "view.html"}


def test_every_label_key_used_exists(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)
    for tile in view["tiles"]:
        for field in tile["fields"]:
            assert field["label"] in system_view.LABELS
        reason = tile["reason"]
        if reason is not None:
            assert reason["v"] in system_view.LABELS


def test_map_md_documents_view_and_the_scheduled_invocation():
    text = (ROOT / ".claude" / "commands" / "map.md").read_text(encoding="utf-8")
    assert "system_map.py view" in text
    assert "--leg scheduled" in text


def test_harness_batch_close_carries_the_full_leg_step():
    data = yaml.safe_load((ROOT / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    moment = next(item for item in data["moments"] if item["name"] == "batch-close")
    organ = next(
        item for item in moment["organs"] if item["id"] == "system_view_full"
    )
    assert organ["optional"] is True
    assert organ["continue_on_failure"] is True
    assert organ["always"] is True
    assert "ADR-133" in organ["reason"]
    assert "RATIFICATION-2026-11-01-ADR-133" in organ["reason"]
    assert ["scripts/system_map.py", "view", "--leg", "full"] == [
        item for item in organ["command"] if item in {
            "scripts/system_map.py",
            "view",
            "--leg",
            "full",
        }
    ]
    assert any("{receipts}" in item for item in organ["command"])


@pytest.mark.parametrize("leg", ["fast", "scheduled"])
def test_assembled_at_and_leg_are_cells_with_a_reader_id(tmp_path, monkeypatch, leg):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW, leg=leg)

    assert view["assembled_at"] == {"v": NOW.isoformat(timespec="seconds"), "r": "assembly"}
    assert view["leg"] == {"v": leg, "r": "assembly"}
    assert set(view["readers"]) == set(READER_IDS) | {"assembly"}
    assert system_view.check_provenance(view) is None


@pytest.mark.parametrize("field", ["leg", "assembled_at"])
@pytest.mark.parametrize("invalid", ["bare", "unknown-reader"])
def test_check_provenance_refuses_a_bare_top_level_value(
    field, invalid, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)
    value = view[field].get("v") if isinstance(view[field], dict) else view[field]
    if invalid == "bare":
        view[field] = value
    else:
        view[field] = {"v": value, "r": "nope"}

    with pytest.raises(system_view.ProvenanceError):
        system_view.check_provenance(view)


def test_quota_with_a_malformed_measured_is_unreadable(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    path = Path(os.environ["DEV_KNOWLEDGE_QUOTA_READS_LEDGER"])
    _write(
        path,
        json.dumps(
            {
                "group": "g",
                "cycle": "2026-11-01",
                "used": 1.0,
                "quota": 10.0,
                "pct": 10.0,
                "measured": "not-a-time",
            }
        )
        + "\n",
    )

    tile = _tile("quota", root)
    assert tile["state"]["v"] == "UNREADABLE"
    assert tile["reason"]["v"] == "unparseable"


def test_quota_count_is_the_source_total_not_the_shown_rows(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    path = Path(os.environ["DEV_KNOWLEDGE_QUOTA_READS_LEDGER"])
    lines = [
        {
            "group": "g",
            "cycle": "2026-11-01",
            "used": 1.0,
            "quota": 10.0,
            "pct": 10.0,
            "measured": NOW.isoformat(),
        }
        for _ in range(15)
    ]
    _write(path, "".join(json.dumps(line) + "\n" for line in lines))

    tile = _tile("quota", root)
    count = next(field["cell"]["v"] for field in tile["fields"] if field["label"] == "count")
    assert count == 15
    assert len(tile["rows"]) == 12


def test_schema_and_thresholds_are_cells_with_the_assembly_reader_id(
    tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)

    assert view["schema"]["v"] == system_view.SCHEMA
    assert view["schema"]["r"] == "assembly"
    assert all(
        isinstance(cell, dict) and cell["r"] == "assembly"
        for cell in view["thresholds"].values()
    )
    assert {
        key: cell["v"] for key, cell in view["thresholds"].items()
    } == system_view.THRESHOLDS


@pytest.mark.parametrize(
    "mutation",
    [
        "field-cell",
        "row-cell",
        "schema",
        "threshold",
        "extra-key",
        "mermaid-url",
        "tile-source",
    ],
)
def test_check_provenance_is_exhaustive_over_bare_scalars(
    mutation, tmp_path, monkeypatch
):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = json.loads(json.dumps(system_view.assemble(root, now=NOW)))

    if mutation == "field-cell":
        tile = next(tile for tile in view["tiles"] if tile["fields"])
        tile["fields"][0]["cell"] = "raw"
    elif mutation == "row-cell":
        tile = next(tile for tile in view["tiles"] if tile["rows"])
        tile["rows"][0][0] = "raw"
    elif mutation == "schema":
        view["schema"] = "raw"
    elif mutation == "threshold":
        view["thresholds"][next(iter(view["thresholds"]))] = 0
    elif mutation == "extra-key":
        view["extra"] = "x"
    elif mutation == "mermaid-url":
        view["mermaid"]["url"] = "raw"
    elif mutation == "tile-source":
        view["tiles"][0]["source"] = "raw"

    with pytest.raises(system_view.ProvenanceError):
        system_view.check_provenance(view)


def test_check_provenance_accepts_the_unmutated_view(tmp_path, monkeypatch):
    root = _fixture_repo(tmp_path, monkeypatch)
    view = system_view.assemble(root, now=NOW)

    assert system_view.check_provenance(view) is None
    html = system_view.render_html(view)
    assert isinstance(html, str)
    assert view["labels"]["title"] in html
